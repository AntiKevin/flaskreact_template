import Cookies from 'js-cookie';
import React, { createContext, useState } from 'react';
import { API_BASE_URL } from '../config/constants';

// Crie o contexto de autenticação
export const AuthContext = createContext();

// Crie o provedor de autenticação
export const AuthProvider = ({ children }) => {

    //get token
    const [token, _setToken] = useState(Cookies.get('access_token'))
    // set token
    const setToken = (data) => {
        Cookies.set('access_token', data);
        _setToken(data);
    }
    // remove token
    const removeToken = () => { 
        Cookies.remove('access_token');
        _setToken(null);
     }


    //get refresh token
    const [refreshToken, _setRefreshToken] = useState(Cookies.get('refresh_token'))
    // set refresh token
    const setRefreshToken = (data) => {
        Cookies.set('refresh_token', data);
        _setRefreshToken(data);
    }
    // remove refresh token
    const removeRefreshToken = () => { 
        Cookies.remove('refresh_token'); 
        _setRefreshToken(null);
    }

    // Função para fazer login e obter os tokens
    const login = async (username, password) => {
        try {
            // Faça a chamada para a sua API de login e obtenha o token JWT
            const response = await fetch(`${API_BASE_URL}/auth/token`, {
                method: 'POST',
                body: JSON.stringify({ username, password }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                setToken(data.access_token);
                setRefreshToken(data.refresh_token);
            } else {
                throw new Error(response.data.detail || 'Erro ao fazer login');
            }
        } catch (error) {
            console.error(error);
        }
    };

    // Função para fazer logout
    const logout = () => {
        removeRefreshToken();
        removeToken();
    };

    const refreshTokens = async () => {
        const response = await fetch(`${API_BASE_URL}/auth/refresh-token`, {
            method: 'POST',
            body: JSON.stringify({ refreshToken }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            setToken(data.access_token);
            setRefreshToken(data.refresh_token);
        } else {
            logout();
            throw new Error(response.data.detail || 'Erro ao atualizar o token de acesso');
        }
    }

    const getLoggedUser = async () => {
        const response = await fetch(`${API_BASE_URL}/auth/logged-user`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        })

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error(response.data.detail || 'Erro ao obter o usuário logado');
        }
    
    }

    // Valor do contexto
    const authContextValue = {
        token,
        setToken,
        refreshToken,
        setRefreshToken,
        refreshTokens,
        login,
        logout,
        getLoggedUser
    };

    // Renderize o provedor de autenticação com o contexto
    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};