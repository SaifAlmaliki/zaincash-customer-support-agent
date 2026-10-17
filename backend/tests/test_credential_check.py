"""Jev adapter tests use the existing runnable shape and real SDK question models."""
import asyncio
from types import SimpleNamespace

import pytest
from langchain_typesafe import Noul, NoulCriteria
from langchain_typesafe.client import (
    TypeSafeAPIConnectionError,
    TypeSafeAPIError,
    TypeSafeAPIResponseValidationError,
    TypeSafeAPITimeoutError,
)

from app.pipeline.stage6_draft.credentials import (
    CredentialCheck,
    DegradedCredentialChecker,
    JevCredentialChecker,
)
from tests.fakes import FakeJevRunnable


class ResponseRunnable:
    """External boundary: deterministic malformed/provider outputs without network."""

    def __init__(self, response):
        self.response = response

    async def ainvoke(self, request):
        return self.response


@pytest.mark.parametrize("value", [0, 0.199, 0.2, 1])
async def test_single_noul_request_preserves_score_and_token_cost(value):
    runnable = FakeJevRunnable(flags={"requests_credentials": value})
    checker = JevCredentialChecker(runnable, price_in_per_m=0.042)
    reply = "لا تشارك الرمز ويا غيرنا. أرسل لنا رمز OTP."
    result = await checker.check(reply)
    assert result.requests_credentials == value and result.degraded is False
    assert result.cost_usd == pytest.approx(0.000042)
    assert len(runnable.calls) == 1
    request = runnable.calls[0]
    assert request["state"] == {"reply_ar": reply}
    assert list(request["questions"]) == ["requests_credentials"]
    question = request["questions"]["requests_credentials"]
    assert isinstance(question, Noul) and isinstance(question.criteria, NoulCriteria)
    assert "disclos" in question.instructions.lower()
    assert "warn" in question.criteria.false.lower()


@pytest.mark.parametrize("bad", [None, float("nan"), float("inf"), -float("inf"), -0.1,
                                 1.1, True, "0.1", "garbage", [], {}, 10**400])
async def test_malformed_noul_degrades_without_losing_measured_cost(bad):
    runnable = FakeJevRunnable(flags={"requests_credentials": bad})
    result = await JevCredentialChecker(runnable, price_in_per_m=0.042).check("دزلي الرمز")
    assert result.requests_credentials is None and result.degraded is True
    assert result.cost_usd == pytest.approx(0.000042)


@pytest.mark.parametrize("nouls", [None, {}, [], {"requests_credentials": None},
                                  {"requests_credentials": SimpleNamespace()}])
async def test_missing_answer_degrades_with_usage(nouls):
    runnable = ResponseRunnable(SimpleNamespace(nouls=nouls, usage={"input_tokens": 2000}))
    result = await JevCredentialChecker(runnable, price_in_per_m=0.042).check("مرحبا")
    assert result.requests_credentials is None and result.degraded is True
    assert result.cost_usd == pytest.approx(0.000084)


@pytest.mark.parametrize("response", [None, {}, "invalid"])
async def test_missing_response_is_explicitly_degraded(response):
    result = await JevCredentialChecker(ResponseRunnable(response), price_in_per_m=0.042).check("مرحبا")
    assert result == CredentialCheck(None, True, 0.0)


@pytest.mark.parametrize("error", [
    TypeSafeAPIError(429, {}, {}),
    TypeSafeAPIConnectionError("connection failed"),
    TypeSafeAPITimeoutError(1),
    TypeSafeAPIResponseValidationError(200, {"usage": {"input_tokens": 3000}}, {}, "answers"),
])
async def test_provider_errors_degrade_and_validation_errors_recover_usage(error):
    result = await JevCredentialChecker(FakeJevRunnable(raises=error), price_in_per_m=0.042).check("مرحبا")
    expected_cost = 0.000126 if isinstance(error, TypeSafeAPIResponseValidationError) else 0.0
    assert result == CredentialCheck(None, True, expected_cost)


async def test_provider_exception_cost_is_preserved_once():
    error = TypeSafeAPIError(503, {"usage": {"input_tokens": 3000}}, {})
    error.cost_usd = 0.005
    result = await JevCredentialChecker(FakeJevRunnable(raises=error), price_in_per_m=0.042).check("مرحبا")
    assert result == CredentialCheck(None, True, 0.005)


async def test_cancellation_propagates_with_cost_for_outer_timeout_owner():
    error = asyncio.CancelledError()
    error.cost_usd = 0.002
    with pytest.raises(asyncio.CancelledError) as caught:
        await JevCredentialChecker(FakeJevRunnable(raises=error), price_in_per_m=0.042).check("مرحبا")
    assert caught.value is error and caught.value.cost_usd == 0.002


async def test_programming_errors_are_not_hidden_as_provider_unavailability():
    with pytest.raises(RuntimeError, match="programming bug"):
        await JevCredentialChecker(FakeJevRunnable(raises=RuntimeError("programming bug")),
                                   price_in_per_m=0.042).check("مرحبا")


@pytest.mark.parametrize("usage", [None, {}, {"input_tokens": -1}, {"input_tokens": float("nan")},
                                  {"input_tokens": "oops"}, {"input_tokens": True},
                                  {"input_tokens": 10**400}])
async def test_bad_usage_cannot_poison_cost(usage):
    response = SimpleNamespace(nouls={"requests_credentials": SimpleNamespace(noul=0.1)}, usage=usage)
    result = await JevCredentialChecker(ResponseRunnable(response), price_in_per_m=0.042).check("مرحبا")
    assert result == CredentialCheck(0.1, False, 0.0)


async def test_unavailable_checker_is_explicit_and_never_invents_a_safe_score():
    checker = DegradedCredentialChecker()
    assert await checker.check("لا تشارك الرقم السري") == CredentialCheck(None, True, 0.0)
    assert await checker.check("دزلي الرقم السري") == CredentialCheck(None, True, 0.0)


@pytest.mark.parametrize("price", [-1, float("inf"), float("nan"), True])
def test_invalid_price_is_a_configuration_error(price):
    with pytest.raises(ValueError):
        JevCredentialChecker(FakeJevRunnable(), price_in_per_m=price)
