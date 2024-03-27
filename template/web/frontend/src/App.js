import React, { lazy, useContext } from 'react'
import { Redirect, Route, BrowserRouter as Router, Switch } from 'react-router-dom'
import AccessibleNavigationAnnouncer from './components/AccessibleNavigationAnnouncer'
import AuthLayout from './containers/AuthLayout'
import { AuthContext } from './context/AuthContext'
import { ToastProvider } from './context/ToastContext'

const Layout = lazy(() => import('./containers/Layout'))

function App() {
  const authContext = useContext(AuthContext)

  return (
    <>
      <Router>
        <AccessibleNavigationAnnouncer />
        <ToastProvider>
        <Switch>
          {/* redirecionar para /app se estiver autenticado ou para /auth/login se não estiver */}
          { authContext.refreshToken ? 
          <Redirect exact from="/auth/login" to="/app" /> 
          : 
          <Redirect from="/app" to="/auth/login" />
          }

          {/* Place new routes over this */}
          <Route path="/app" component={Layout} />
          {/* Place new routes over this */}
          <Route path="/auth" component={AuthLayout} />
          {/* If you have an index page, you can remothis Redirect */}
          <Redirect exact from="/" to="/app/dashboard" />
        </Switch>
        </ToastProvider>
      </Router>
    </>
  )
}

export default App
