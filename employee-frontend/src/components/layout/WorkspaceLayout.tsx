import { Suspense, useState } from "react"
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom"
import {
  Inbox,
  Layers3,
  BookOpen,
  ChartNoAxesCombined,
  FlaskConical,
  ChevronDown,
  ChevronRight,
  PanelLeftClose,
  Menu,
  Plus,
  Radio,
  ShieldCheck,
  CircleHelp,
  ArrowUpRight,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { useWorkspace } from "@/lib/workspace"
import { useCopy } from "@/lib/locale"
import { LoadingState } from "@/components/shared/workspace-ui"
import { LanguageToggle } from "@/components/layout/LanguageToggle"

const navigation = [
  { to: "/", key: "queue", icon: Inbox },
  { to: "/runs", key: "runs", icon: Layers3 },
  { to: "/knowledge", key: "knowledge", icon: BookOpen },
  { to: "/insights", key: "insights", icon: ChartNoAxesCombined },
  { to: "/evaluation", key: "evaluation", icon: FlaskConical },
] as const

export function WorkspaceLayout() {
  const workspace = useWorkspace()
  const copy = useCopy()
  const [menu, setMenu] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const current = navigation.find(
    (item) => item.to !== "/" && location.pathname.startsWith(item.to)
  )
  const section = current ? copy.nav[current.key] : copy.nav.queue
  return (
    <div className="workspace-app">
      <a className="skip-link" href="#main-content">
        {copy.layout.skip}
      </a>
      {menu && (
        <button
          className="sidebar-backdrop"
          aria-label={copy.layout.closeNav}
          onClick={() => setMenu(false)}
        />
      )}
      <aside className={`workspace-sidebar ${menu ? "sidebar-open" : ""}`}>
        <div className="brand">
          <span className="brand-symbol">
            <span />
            <span />
            <span />
          </span>
          <div>
            zain<span>cash</span>
            <small>{copy.layout.workspaceName}</small>
          </div>
          <Button
            className="mobile-only"
            variant="ghost"
            size="icon"
            aria-label={copy.layout.closeNav}
            onClick={() => setMenu(false)}
          >
            <PanelLeftClose size={18} />
          </Button>
        </div>
        <div className="workspace-switch">
          <span className="workspace-initials">ZC</span>
          <span>
            <strong>{copy.layout.customerSupport}</strong>
            <small>{copy.layout.iraq}</small>
          </span>
          <ChevronDown size={15} />
        </div>
        <div className="nav-section-label">{copy.layout.section}</div>
        <nav aria-label={copy.layout.section}>
          {navigation.map((item) => (
            <NavLink
              end={item.to === "/"}
              key={item.to}
              to={item.to}
              onClick={() => setMenu(false)}
              className={({ isActive }) =>
                `nav-item ${isActive ? "nav-active" : ""}`
              }
            >
              <item.icon size={18} strokeWidth={1.7} />
              <span>{copy.nav[item.key]}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-note">
          <ShieldCheck size={19} />
          <strong>{copy.layout.promiseTitle}</strong>
          <p>{copy.layout.promiseBody}</p>
        </div>
        <div className="sidebar-bottom">
          <a
            href="/api/docs"
            target="_blank"
            rel="noreferrer"
            className="nav-item"
          >
            <CircleHelp size={18} />
            {copy.layout.apiDocs}
            <ArrowUpRight size={14} />
          </a>
          <div className="hackathon-label">
            <span>06</span>
            <div>
              <strong>{copy.layout.challengeTitle}</strong>
              <small>{copy.layout.challengeMeta}</small>
            </div>
          </div>
        </div>
      </aside>
      <div className="workspace-main">
        <header className="workspace-topbar">
          <div className="breadcrumbs">
            <Button
              className="mobile-only"
              variant="ghost"
              size="icon"
              aria-label={copy.layout.openNav}
              aria-expanded={menu}
              onClick={() => setMenu(true)}
            >
              <Menu size={20} />
            </Button>
            <span>{copy.layout.section}</span>
            <ChevronRight size={14} />
            <strong>{section}</strong>
          </div>
          <div className="topbar-actions">
            <span
              className={`connection-status ${workspace.health && !workspace.connectionError ? "is-connected" : ""}`}
            >
              <Radio size={13} />
              {workspace.connectionError
                ? copy.layout.offline
                : workspace.health
                  ? copy.layout.connected
                  : copy.layout.connecting}
            </span>
            <Tooltip>
              <TooltipTrigger
                render={<span className="reviewer-avatar" tabIndex={0} />}
              >
                SA
              </TooltipTrigger>
              <TooltipContent>{copy.layout.reviewer}</TooltipContent>
            </Tooltip>
            <LanguageToggle />
          </div>
        </header>
        <main id="main-content" className="workspace-content">
          <Suspense fallback={<LoadingState />}>
            <Outlet />
          </Suspense>
        </main>
        <footer className="workspace-footer">
          <span>
            <ShieldCheck size={13} />
            {copy.layout.footerApproval}
          </span>
          <span>{copy.layout.footerTopic}</span>
        </footer>
        <Button
          className="mobile-new-batch"
          aria-label={copy.layout.newBatch}
          onClick={() => navigate("/runs/new")}
        >
          <Plus size={20} />
        </Button>
      </div>
    </div>
  )
}
