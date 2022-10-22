import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function AlertDialog(props) {
	return (
		<Dialog
			open={props.handleAlertDialog}
			onClose={props.handleCloseAlert}
			aria-labelledby='alert-dialog-title'
			aria-describedby='alert-dialog-description'
		>
			<DialogTitle id='alert-dialog-title'>{`${props.alertTitle}`}</DialogTitle>
			<DialogContent>
				<DialogContentText id='alert-dialog-description'>
					{`${props.alertDesc}`}
				</DialogContentText>
			</DialogContent>
			<DialogActions
				sx={{
					m: 1,
				}}
			>
				<Button onClick={props.handleCloseAlert}>Cancel</Button>
				<Button onClick={props.handleSubmitAlert} variant='contained' autoFocus>
					Proceed
				</Button>
			</DialogActions>
		</Dialog>
	);
}