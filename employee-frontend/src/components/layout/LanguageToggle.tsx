import { useLocale } from "@/lib/locale"
import type { Locale } from "@/lib/locale"

export function LanguageToggle() {
  const { locale, setLocale, copy } = useLocale()
  const choose = (next: Locale) => {
    if (next !== locale) setLocale(next)
  }
  return (
    <div className="lang-toggle" role="group" aria-label={copy.toggle.group}>
      <button type="button" data-locale="ar" aria-pressed={locale === "ar"} aria-label={copy.toggle.arabic} onClick={() => choose("ar")}>
        ع
      </button>
      <button type="button" data-locale="en" aria-pressed={locale === "en"} aria-label={copy.toggle.english} onClick={() => choose("en")}>
        EN
      </button>
    </div>
  )
}
