import * as React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useSelector } from 'react-redux';
import Spinner from '../components/Spinner';

const lightTheme = createTheme({
	palette: {
		background: {
			default: '#f2f2f2',
		},
	},
});

const darkTheme = createTheme({
	palette: {
		mode: 'dark',
	},
});

export default function CustomThemeProvider({ children }) {
	const { isLoading } = useSelector((state) => state.auth);

	var localIsDarkMode = JSON.parse(localStorage.getItem('isDarkMode'));

	if (isLoading) {
		return <Spinner />;
	}

	return (
		<ThemeProvider theme={localIsDarkMode ? darkTheme : lightTheme}>
			{children}
		</ThemeProvider>
	);
}