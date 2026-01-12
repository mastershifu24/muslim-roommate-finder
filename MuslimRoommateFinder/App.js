import React from 'react';
import { StatusBar } from 'expo-status-bar';
// TEMPORARY: Comment out AuthProvider to test
// import { AuthProvider } from './src/context/AuthContext';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  return (
    // <AuthProvider>
      <>
        <StatusBar style="auto" />
        <AppNavigator />
      </>
    // </AuthProvider>
  );
}
