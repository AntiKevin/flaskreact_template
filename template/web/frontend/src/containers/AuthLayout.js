import React, { Suspense, lazy } from 'react'
import { Redirect, Route, Switch } from 'react-router-dom'
import routes from '../routes/auth'

import ThemedSuspense from '../components/ThemedSuspense'

const Page404 = lazy(() => import('../pages/404'))

function AuthLayout() {

  return (
    <main className="h-full overflow-y-auto">
      <Suspense fallback={<ThemedSuspense />}>
            <Switch>
              {routes.map((route, i) => {
                return route.component ? (
                  <Route
                    key={i}
                    exact={true}
                    path={`/auth${route.path}`}
                    render={(props) => <route.component {...props} />}
                  />
                ) : null
              })}
              <Redirect exact from="/app" to="/app/dashboard" />
              <Route component={Page404} />
            </Switch>
          </Suspense>
    </main> 
  )
}

export default AuthLayout
