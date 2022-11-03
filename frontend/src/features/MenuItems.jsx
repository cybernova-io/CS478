import * as React from 'react';
import { useState } from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import IconButton from '@mui/material/IconButton';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import EditPostForm from '../../components/post/EditPostForm';
import DeleteDialog from '../../components/alert-box/DeleteDialog';

export default function MenuItems(props) {
	const [editPostForm, setEditPostForm] = useState(false);

	const [deleteDialog, setdeleteDialog] = React.useState(false);

	const [anchorEl, setAnchorEl] = React.useState(null);

	const openOptions = Boolean(anchorEl);

	const handleClickOptions = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const handleCloseOptions = () => {
		setAnchorEl(null);
	};

	const handleDeleteDialog = () => {
		setdeleteDialog((prevData) => !prevData);
	};

	const toggleEditPostModal = () => {
		setEditPostForm((prevData) => !prevData);
	};

	// Identify component type
	let onClickEditMenu;

	if (props.componentType === 'post') {
		onClickEditMenu = toggleEditPostModal;
	} else if (props.componentType === 'comment') {
		onClickEditMenu = () => props.componentFunc(props.componentData._id);
	}

	return (
		<>
			<IconButton
				aria-label='more'
				id='long-button'
				aria-controls={openOptions ? 'long-menu' : undefined}
				aria-expanded={openOptions ? 'true' : undefined}
				aria-haspopup='true'
				onClick={handleClickOptions}
			>
				<MoreVertIcon />
			</IconButton>
			<Menu
				id='long-menu'
				MenuListProps={{
					'aria-labelledby': 'menu-button',
				}}
				anchorEl={anchorEl}
				open={openOptions}
				onClose={handleCloseOptions}
				PaperProps={{
					style: {
						width: '20ch',
					},
				}}
			>
				<MenuItem onClick={onClickEditMenu}>
					<ListItemIcon>
						<EditIcon fontSize='small' />
					</ListItemIcon>
					<ListItemText>Edit</ListItemText>
				</MenuItem>
				<EditPostForm
					key={props.componentData._id}
					editPostForm={editPostForm}
					toggleEditPostModal={toggleEditPostModal}
					handleCloseOptions={handleCloseOptions}
					postData={props.componentData}
				/>
				<MenuItem onClick={handleDeleteDialog}>
					<ListItemIcon>
						<DeleteIcon fontSize='small' />
					</ListItemIcon>
					<ListItemText>Delete</ListItemText>
				</MenuItem>
				<DeleteDialog
					deleteDialog={deleteDialog}
					componentData={props.componentData}
					componentType={props.componentType}
					handleDeleteDialog={handleDeleteDialog}
				/>
			</Menu>
		</>
	);
}