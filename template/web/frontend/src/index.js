import { Windmill } from '@windmill/react-ui'
import React, { Suspense } from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import './assets/css/tailwind.output.css'
import ThemedSuspense from './components/ThemedSuspense'
import { AuthProvider } from './context/AuthContext'
import { SidebarProvider } from './context/SidebarContext'
import * as serviceWorker from './serviceWorker'

// if (process.env.NODE_ENV !== 'production') {
//   const axe = require('react-axe')
//   axe(React, ReactDOM, 1000)
// }

ReactDOM.render(
  <AuthProvider>
  <SidebarProvider>
    <Suspense fallback={<ThemedSuspense />}>
      <Windmill usePreferences>
        <App />
      </Windmill>
    </Suspense>
  </SidebarProvider>
  </AuthProvider>,
  document.getElementById('root')
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register()
