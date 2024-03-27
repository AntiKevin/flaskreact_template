import Alert from '@mui/material/Alert';
import Slide from '@mui/material/Slide';
import Snackbar from '@mui/material/Snackbar';
import React, { createContext, useState } from 'react';

export const ToastContext = createContext();

export const ToastProvider = ({ children }) => {
    const [toastMessage, setToastMessage] = useState('');
    const [toastOpen, setToastOpen] = useState(false);
    const [type, setType] = useState('')

    const showToast = (message, type) => {
        setToastMessage(message);
        setType(type);
        setToastOpen(true);
    };

    const hideToast = () => {
        setToastOpen(false);
    };

    return (
        
        <ToastContext.Provider value={{ showToast, hideToast }}>
            {children}
            <Snackbar 
            open={toastOpen}
            TransitionComponent={Slide} 
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            autoHideDuration={6000}
            onClose={hideToast} 
            >
                <Alert
                    severity={type}
                    variant="filled"
                    sx={{ width: '100%' }}
                >
                    {toastMessage}
                </Alert>
            </Snackbar>
        </ToastContext.Provider>
    );
};