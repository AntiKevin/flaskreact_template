import Cookies from 'js-cookie';
import jwt from 'jsonwebtoken';
import React, { useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';

function ThemedSuspense() {
  const authContext = useContext(AuthContext);

  useEffect(() => {
    // Obtenha o token do cookie
    let token = Cookies.get('token');

    if (token) {
      console.log('Token:', token);
      // Decodifique o token para obter a data de expiração
      let decodedToken = jwt.decode(token);
      let expirationDate = new Date(decodedToken.exp * 1000);
      let currentDate = new Date();

      // Verifique se o token expirou
      if (expirationDate < currentDate) {
        // Solicite um novo token ao servidor
        // Supondo que você tenha uma função refreshToken() que faz isso
        authContext.refreshTokens()
      }
    }

  }, []);

  return (
    <div className="w-full h-screen p-6 text-lg font-medium text-gray-600 dark:text-gray-400 dark:bg-gray-900">
      Loading...
    </div>
  )
}

export default ThemedSuspense
