# React Navigation + React 19 Compatibility Issue

```
React Navigation 7.9.1 with React 19.1.0 - TypeError: expected dynamic type 'boolean', but had type 'string'
```

## Error
```
TypeError: expected dynamic type 'boolean', but had type 'string'
```

## Expected Behavior
The app should render successfully with React Navigation, displaying the TestScreen component without any errors. The navigation should work normally.

## Actual Behavior
The app crashes immediately on launch with a TypeError indicating that React Navigation is trying to pass a string value where a boolean is expected to a native component. The error occurs during the initial render, before any user interaction.

## Environment
- **React**: 19.1.0
- **React Native**: 0.81.5
- **React Navigation Native**: 7.1.27
- **React Navigation Native Stack**: 7.9.1
- **React Navigation Bottom Tabs**: 7.9.1
- **Expo SDK**: 54.0.31
- **Platform**: iOS (Expo Go)

## Minimal Reproduction

### AppNavigator.js
```javascript
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import TestScreen from '../screens/TestScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Test" 
          component={TestScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### TestScreen.js
```javascript
import React from 'react';
import { View, Text } from 'react-native';

export default function TestScreen({ navigation, route }) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Test Screen - Minimal</Text>
    </View>
  );
}
```

### App.js
```javascript
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  return (
    <>
      <StatusBar style="auto" />
      <AppNavigator />
    </>
  );
}
```

## What We've Tried

1. ✅ Normalized all boolean props (headerShown, gestureEnabled, etc.)
2. ✅ Ensured all boolean values are explicit (`false` not `"false"`)
3. ✅ Minimal test screen with no props
4. ✅ Removed AuthProvider and all hooks
5. ✅ Updated React Navigation to latest versions
6. ✅ Tested with React 18.3.1 - got DIFFERENT error (module resolution), confirming React 19 is the issue
7. ✅ Verified all screen options are proper booleans

## Stack Trace
```
ERROR  [Error: Exception in HostFunction: TypeError: expected dynamic type 'boolean', but had type 'string']
    at createNode (native)
    at completeWork
    at runWithFiberInDEV
    at completeUnitOfWork
    at performUnitOfWork
    at workLoopSync
    at renderRootSync
    at performWorkOnRoot
    at performWorkOnRootViaSchedulerTask
```

## Notes
- Error occurs even with absolute minimum setup (no options, no props, just basic navigation)
- Works with React 18 (but React Native 0.81.5 requires React 19)
- Suggests React Navigation 7.x may not be fully compatible with React 19

## Where to Report
- **React Navigation GitHub**: https://github.com/react-navigation/react-navigation/issues
- **React Native GitHub**: https://github.com/facebook/react-native/issues
- **Expo GitHub**: https://github.com/expo/expo/issues

