import * as React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Avatar from '@mui/material/Avatar';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import userService from '../../src/features/users/usersService';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
	'& .MuiDialogContent-root': {
		padding: theme.spacing(2),
		width: 600,
	},
	'& .MuiDialogActions-root': {
		padding: theme.spacing(1),
	},
}));

const BootstrapDialogTitle = (props) => {
	const { children, onClose, ...other } = props;

	return (
		<DialogTitle sx={{ m: 0, p: 2 }} {...other}>
			{children}
			{onClose ? (
				<IconButton
					aria-label='close'
					onClick={onClose}
					sx={{
						position: 'absolute',
						right: 8,
						top: 8,
						color: (theme) => theme.palette.grey[500],
					}}
				>
					<CloseIcon />
				</IconButton>
			) : null}
		</DialogTitle>
	);
};

BootstrapDialogTitle.propTypes = {
	children: PropTypes.node,
	onClose: PropTypes.func.isRequired,
};

export default function LikesModal(props) {
	const { user } = useSelector((state) => state.auth);

	const [likesData, setLikesData] = useState([]);

	const getUserDetails = async () => {
		props.likesUserId.map(async (userId) => {
			const userData = await userService.getUserDataById(userId, user.token);
			setLikesData([
				{
					userId: userData._id,
					lastName: userData.lastName,
					firstName: userData.firstName,
				},
			]);
		});
	};

	useEffect(() => {
		getUserDetails();
	}, [props.likesUserId]);

	return (
		<BootstrapDialog
			onClose={props.closeLikesModal}
			aria-labelledby='customized-dialog-title'
			open={props.likesModal}
		>
			<BootstrapDialogTitle
				id='customized-dialog-title'
				onClose={props.closeLikesModal}
			>
				Likes
			</BootstrapDialogTitle>
			<DialogContent dividers>
				<List dense sx={{ width: '100%', maxHeight: 350 }}>
					{likesData.map((data) => {
						const labelId = `checkbox-list-secondary-label-${data.userId}`;
						return (
							<ListItem
								key={data.userId}
								secondaryAction={
									data.userId !== user._id && (
										<Button
											variant='outlined'
											startIcon={<PersonAddIcon />}
											component='span'
											sx={{ textTransform: 'capitalize' }}
										>
											Add Friend
										</Button>
									)
								}
								disablePadding
							>
								<ListItemButton>
									<ListItemAvatar>
										<Avatar
											alt={`Avatar n°${data.userId + 1}`}
											src={`/static/images/avatar/${data.userId + 1}.jpg`}
										/>
									</ListItemAvatar>
									<ListItemText
										id={labelId}
										primary={`${data.firstName} ${data.lastName}`}
									/>
								</ListItemButton>
							</ListItem>
						);
					})}
				</List>
			</DialogContent>
		</BootstrapDialog>
	);
}