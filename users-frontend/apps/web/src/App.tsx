import { IntakePage } from "./features/intake/IntakePage"
import { createIntakeApi } from "./features/intake/api"
import { IntakeController } from "./features/intake/controller"
import { browserSessionStorage } from "./features/intake/session"

const controller = new IntakeController(createIntakeApi(), browserSessionStorage())

export function App() {
  return <IntakePage controller={controller} />
}
