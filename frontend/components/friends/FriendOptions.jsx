import * as React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import DialogTitle from "@mui/material/DialogTitle";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import friendService from "../../../src/features/friends/friendService";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import { Typography } from "@mui/material";
import AlertDialog from "../../alert-box/AlertDialog";
import Skeleton from "@mui/material/Skeleton";

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

export default function FriendOptions(props) {
  const { user } = useSelector((state) => state.auth);
  const [unFriendDialog, setUnFriendDialog] = React.useState(false);

  const [friendsData, setFriendsData] = useState([]);

  // Get user friends (array)
  const getFriendOptions = async () => {
    const userFriendsList = await friendService.getUserFriends(user.token);

    var friendDataArray = await Promise.all(
      userFriendsList.map(async (friendsId) => {
        const friendData = await friendService.getFriendsDataById(
          friendsId,
          user.token
        );

        return {
          recipient: friendData ? friendData.recipient : "",
          requester: friendData ? friendData.requester : "",
          status: friendData ? friendData.status : "",
        };
      })
    );
    if (friendDataArray.length === 0) {
      friendDataArray = [
        {
          recipient: "",
          requester: "",
          status: "",
        },
      ];
    }
    setFriendsData(friendDataArray);
  };

  useEffect(() => {
    getFriendOptions();
  }, []);

  // Send friend request
  const handleSendFriendRequest = async (userB) => {
    var friendRequestData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.sendFriendRequest(friendRequestData, user.token);
    getFriendOptions();
  };

  // Cancel or reject friend request
  const handleCancelFriendRequest = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.rejectFriendRequest(friendData, user.token);
    getFriendOptions();
  };

  // Accept friend request
  const handleAcceptFriendRequest = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.acceptFriendRequest(friendData, user.token);

    getFriendOptions();
  };

  const handleUnFriendDialog = () => {
    setUnFriendDialog((prevData) => !prevData);
  };

  const handleUnFriendSubmit = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };
    await friendService.unFriend(friendData, user.token);
    if (props.component === "allFriends") {
      props.componentFunc();
    }
  };

  var buttonAction;

  var isFriend = friendsData.some(
    (zdata) => zdata.recipient === props.userData._id
  );

  isFriend
    ? friendsData.map((fdata) => {
        if (fdata.recipient === props.userData._id && fdata.status === 1) {
          buttonAction = (
            <Button
              size="small"
              sx={{ textTransform: "capitalize" }}
              onClick={() => handleCancelFriendRequest(props.userData._id)}
            >
              Cancel Request
            </Button>
          );
        } else if (
          fdata.recipient === props.userData._id &&
          fdata.status === 2
        ) {
          buttonAction = (
            <Stack spacing={1} direction="row">
              <Button
                variant="contained"
                size="small"
                sx={{ textTransform: "capitalize" }}
                onClick={() => handleAcceptFriendRequest(props.userData._id)}
              >
                Confirm
              </Button>
              <Button
                size="small"
                sx={{ textTransform: "capitalize" }}
                onClick={() => handleCancelFriendRequest(props.userData._id)}
              >
                Delete
              </Button>
            </Stack>
          );
        } else if (
          fdata.recipient === props.userData._id &&
          fdata.status === 3 &&
          props.component === "likesModal"
        ) {
          buttonAction = (
            <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
              <PeopleAltIcon fontSize="small" sx={{ color: "#808080" }} />
              <Typography sx={{ color: "#808080" }} variant="body2">
                Friend
              </Typography>
            </Stack>
          );
        } else if (
          fdata.recipient === props.userData._id &&
          fdata.status === 3 &&
          props.component === "allFriends"
        ) {
          buttonAction = (
            <>
              <Button
                size="small"
                sx={{ textTransform: "capitalize" }}
                // onClick={() => handleUnFriendDialog(props.userData._id)}
                onClick={handleUnFriendDialog}
              >
                Unfriend
              </Button>
              <AlertDialog
                handleAlertDialog={unFriendDialog}
                alertTitle={`Unfriend?`}
                alertDesc={`Are you sure you want to change the theme?`}
                handleCloseAlert={handleUnFriendDialog}
                handleSubmitAlert={() =>
                  handleUnFriendSubmit(props.userData._id)
                }
              />
            </>
          );
        }
      })
    : (buttonAction = (
        <Button
          variant="contained"
          size="small"
          sx={{ textTransform: "capitalize" }}
          onClick={() => handleSendFriendRequest(props.userData._id)}
        >
          Add Friend
        </Button>
      ));
  return friendsData.length > 0 ? (
    buttonAction
  ) : (
    <Skeleton animation="wave" width="100%" />
  );
}
