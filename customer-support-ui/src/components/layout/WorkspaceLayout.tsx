import { useState } from "react"
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom"
import { Inbox, Layers3, BookOpen, ChartNoAxesCombined, FlaskConical, ChevronDown, ChevronRight, PanelLeftClose, Menu, Plus, Radio, ShieldCheck, CircleHelp, ArrowUpRight, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { useWorkspace } from "@/lib/workspace"
import { FilterSelect } from "@/components/shared/workspace-ui"

const navigation = [
  { to: "/", label: "Support queue", icon: Inbox }, { to: "/runs", label: "Pipeline runs", icon: Layers3 },
  { to: "/knowledge", label: "Knowledge base", icon: BookOpen }, { to: "/insights", label: "Weekly insights", icon: ChartNoAxesCombined },
  { to: "/evaluation", label: "Evaluation", icon: FlaskConical },
]

export function WorkspaceLayout() {
  const workspace = useWorkspace()
  const [menu, setMenu] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const section = navigation.find((item) => item.to !== "/" && location.pathname.startsWith(item.to))?.label || "Support queue"
  const preview = workspace.mode === "preview"
  return <div className="workspace-app">
    <a className="skip-link" href="#main-content">Skip to content</a>
    {menu && <button className="sidebar-backdrop" aria-label="Close navigation" onClick={() => setMenu(false)} />}
    <aside className={`workspace-sidebar ${menu ? "sidebar-open" : ""}`}>
      <div className="brand"><span className="brand-symbol"><span /><span /><span /></span><div>zain<span>cash</span><small>Support workspace</small></div><Button className="mobile-only" variant="ghost" size="icon" aria-label="Close navigation" onClick={() => setMenu(false)}><PanelLeftClose size={18} /></Button></div>
      <div className="workspace-switch"><span className="workspace-initials">ZC</span><span><strong>Customer support</strong><small>Iraq workspace</small></span><ChevronDown size={15} /></div>
      <div className="nav-section-label">Workspace</div>
      <nav aria-label="Main navigation">{navigation.map((item) => <NavLink end={item.to === "/"} key={item.to} to={item.to} onClick={() => setMenu(false)} className={({ isActive }) => `nav-item ${isActive ? "nav-active" : ""}`}>
        <item.icon size={18} strokeWidth={1.7} /><span>{item.label}</span>{item.to === "/" && preview && <span className="nav-count">{workspace.preview.filter((r) => r.status === "pending_review").length}</span>}
      </NavLink>)}</nav>
      <div className="sidebar-note"><ShieldCheck size={19} /><strong>AI prepares. You decide.</strong><p>Every response stays in review until a person approves it.</p></div>
      <div className="sidebar-bottom"><a href="/api/docs" target="_blank" rel="noreferrer" className="nav-item"><CircleHelp size={18} />API documentation<ArrowUpRight size={14} /></a><div className="hackathon-label"><span>06</span><div><strong>Support pipeline automation</strong><small>Agentic AI Challenge Iraq</small></div></div></div>
    </aside>
    <div className="workspace-main">
      <header className="workspace-topbar"><div className="breadcrumbs"><Button className="mobile-only" variant="ghost" size="icon" aria-label="Open navigation" aria-expanded={menu} onClick={() => setMenu(true)}><Menu size={20} /></Button><span>Workspace</span><ChevronRight size={14} /><strong>{section}</strong></div>
        <div className="topbar-actions"><span className={`connection-status ${workspace.health && !workspace.connectionError ? "is-connected" : ""}`}><Radio size={13} />{workspace.connectionError ? "API offline" : workspace.health ? "API connected" : "Connecting…"}</span>
          <FilterSelect label="Workspace data source" value={workspace.mode} options={[{ value: "live", label: "Live workspace" }, { value: "preview", label: "Preview workspace" }]} onChange={(value) => workspace.setMode(value as "live" | "preview")} />
          <Tooltip><TooltipTrigger render={<span className="reviewer-avatar" tabIndex={0} />}>SA</TooltipTrigger><TooltipContent>Local support reviewer</TooltipContent></Tooltip>
        </div>
      </header>
      {preview && <div className="preview-banner"><Sparkles size={14} /><span><strong>Preview workspace</strong> — illustrative synthetic tickets. Changes here stay in this browser session.</span><button onClick={() => workspace.setMode("live")}>Switch to live <ArrowUpRight size={13} /></button></div>}
      <main id="main-content" className="workspace-content"><Outlet /></main>
      <footer className="workspace-footer"><span><ShieldCheck size={13} />Human approval required for every response</span><span>Topic 06 · Built for Iraq</span></footer>
      <Button className="mobile-new-batch" aria-label="New batch" onClick={() => navigate("/runs/new")}><Plus size={20} /></Button>
    </div>
  </div>
}
