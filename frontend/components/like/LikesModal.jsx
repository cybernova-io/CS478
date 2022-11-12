import * as React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";
import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Avatar from "@mui/material/Avatar";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import ListItemSecondaryAction from "@mui/material/ListItemSecondaryAction";
import userService from "../../src/features/users/userService";
import FriendOptions from "../features/friends/FriendOptions";
import UserNameLink from "../../components/features/UserNameLink";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
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
          aria-label="close"
          onClick={onClose}
          sx={{
            position: "absolute",
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

  // Get user details by _id
  const getUserDetails = async () => {
    const userDataArray = await Promise.all(
      props.likesUserId.map(async (userId) => {
        var userData = await userService.getUserDataById(userId, user.token);
        return {
          _id: userData._id,
          lastName: userData.lastName,
          firstName: userData.firstName,
          photo: userData.photo,
        };
      })
    );
    setLikesData(userDataArray);
  };

  useEffect(() => {
    getUserDetails();
  }, [props.likesModal]);

  return (
    <BootstrapDialog
      onClose={props.closeLikesModal}
      aria-labelledby="customized-dialog-title"
      open={props.likesModal}
      fullWidth
    >
      <BootstrapDialogTitle
        id="customized-dialog-title"
        onClose={props.closeLikesModal}
      >
        Likes
      </BootstrapDialogTitle>

      <DialogContent dividers>
        <List dense sx={{ width: "100%", maxHeight: 350 }}>
          {likesData.map((data) => {
            const labelId = `checkbox-list-secondary-label-${data._id}`;

            return (
              <ListItem key={data._id}>
                <ListItemAvatar>
                  <Avatar src={data.photo && `/uploads/${data.photo}`} />
                </ListItemAvatar>
                <ListItemText
                  id={labelId}
                  primary={<UserNameLink data={data} />}
                />
                <ListItemSecondaryAction>
                  {data._id !== user._id ? (
                    <FriendOptions userData={data} component="likesModal" />
                  ) : (
                    " "
                  )}
                </ListItemSecondaryAction>
              </ListItem>
            );
          })}
        </List>
      </DialogContent>
    </BootstrapDialog>
  );
}
