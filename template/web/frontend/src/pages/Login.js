import React, { useContext } from 'react'
import { Link } from 'react-router-dom'

import { Button, Input, Label } from '@windmill/react-ui'
import { useForm } from "react-hook-form"
import ImageDark from '../assets/img/login-office-dark.jpeg'
import ImageLight from '../assets/img/login-office.jpeg'
import { AuthContext } from '../context/AuthContext'
import { ToastContext } from '../context/ToastContext'

function Login() {
  const authContext = useContext(AuthContext)
  const { showToast } = useContext(ToastContext)

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm()

  const onSubmit = async (data) => {
    await authContext.login(data.username, data.password)
    showToast("login realizado com sucesso", "success")
  }

  return (
    <div className="flex items-center min-h-screen p-6 bg-gray-50 dark:bg-gray-900">
      <div className="flex-1 h-full max-w-4xl mx-auto overflow-hidden bg-white rounded-lg shadow-xl dark:bg-gray-800">
        <div className="flex flex-col overflow-y-auto md:flex-row">
          <div className="h-32 md:h-auto md:w-1/2">
            <img
              aria-hidden="true"
              className="object-cover w-full h-full dark:hidden"
              src={ImageLight}
              alt="Office"
            />
            <img
              aria-hidden="true"
              className="hidden object-cover w-full h-full dark:block"
              src={ImageDark}
              alt="Office"
            />
          </div>
          <main className="flex items-center justify-center p-6 sm:p-12 md:w-1/2">
            <div className="w-full">
            <form onSubmit={handleSubmit(onSubmit)}>
              <h1 className="mb-4 text-xl font-semibold text-gray-700 dark:text-gray-200">Login</h1>
              <Label>
                <span>Username</span>
                <Input className="mt-1" type="username" placeholder="username" {...register("username", { required: true })} />
              </Label>

              <Label className="mt-4">
                <span>Password</span>
                <Input className="mt-1" type="password" placeholder="***************" {...register("password", { required: true })} />
              </Label>

              <Button className="mt-4" block type='sumit'>
                Log in
              </Button>
              </form>

              <hr className="my-8" />

              <p className="mt-4">
              </p>
              <p className="mt-1">
                <Link
                  className="text-sm font-medium text-purple-600 dark:text-purple-400 hover:underline"
                  to="/create-account"
                >
                  Create account
                </Link>
              </p>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default Login
