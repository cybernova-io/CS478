import * as React from "react";
import { useSelector, useDispatch } from "react-redux";
import { Typography } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import MailIcon from "@mui/icons-material/Mail";
import MailOutlinedIcon from "@mui/icons-material/MailOutlined";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Badge from "@mui/material/Badge";
import HomeIcon from "@mui/icons-material/Home";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PublicIcon from "@mui/icons-material/Public";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import BookmarkBorderOutlinedIcon from "@mui/icons-material/BookmarkBorderOutlined";
import { useRouter } from "next/router";
import Link from "next/link";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import DarkModeSwitch from "../features/DarkModeSwitch";
import UserAvatar from "../features/UserAvatar";
import { logout, reset } from "../../src/features/auth/authSlice";
import { reset as postReset } from "../../src/features/posts/postSlice";
import { reset as commentReset } from "../../src/features/comments/commentSlice";
import Divider from "@mui/material/Divider";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import PeopleAltOutlinedIcon from "@mui/icons-material/PeopleAltOutlined";

export default function DrawerMenu(props) {
  const router = useRouter();
  const dispatch = useDispatch();

  const { user } = useSelector((state) => state.auth);

  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const drawerMenu = [
    {
      text: "Home",
      icon: "HomeIcon",
      link: "/home",
    },
    {
      text: "Explore",
      icon: "PublicIcon",
      link: "/explore",
    },
    {
      text: "Friends",
      icon: "PeopleAltIcon",
      link: "/friends",
    },
    // {
    // 	text: 'Notifications',
    // 	icon: 'NotificationsIcon',
    // 	link: '/notifications',
    // },
    {
      text: "Messages",
      icon: "MailIcon",
      link: "/messages",
    },
    {
      text: "Saved",
      icon: "BookmarkIcon",
      link: "/saved",
    },
  ];

  const onLogout = () => {
    dispatch(logout());
    dispatch(reset());
    dispatch(postReset());
    dispatch(commentReset());
    router.push("/");
  };

  const drawer = (
    <List sx={{ display: "flex", flexDirection: "column", height: " 100vh" }}>
      {drawerMenu.map((data) => {
        var activeLink = router.pathname === data.link ? "primary" : "";
        var buttonIcon;

        if (data.icon === "HomeIcon") {
          buttonIcon =
            router.pathname === data.link ? (
              <HomeIcon color="primary" />
            ) : (
              <HomeOutlinedIcon />
            );
        } else if (data.icon === "PublicIcon") {
          buttonIcon = <PublicIcon color={activeLink} />;
        } else if (data.icon === "PeopleAltIcon") {
          buttonIcon =
            router.pathname === data.link ? (
              <PeopleAltIcon color="primary" />
            ) : (
              <PeopleAltOutlinedIcon />
            );
        } else if (data.icon === "NotificationsIcon") {
          buttonIcon = (
            <Badge badgeContent={3} color="error">
              {router.pathname === data.link ? (
                <NotificationsIcon color="primary" />
              ) : (
                <NotificationsOutlinedIcon />
              )}
            </Badge>
          );
        } else if (data.icon === "MailIcon") {
          buttonIcon =
            router.pathname === data.link ? (
              <MailIcon color="primary" />
            ) : (
              <MailOutlinedIcon />
            );
        } else if (data.icon === "BookmarkIcon") {
          buttonIcon =
            router.pathname === data.link ? (
              <BookmarkIcon color="primary" />
            ) : (
              <BookmarkBorderOutlinedIcon />
            );
        }
        return (
          <ListItem key={data.text} disablePadding sx={{ display: "block" }}>
            <Link href={data.link} passHref>
              <ListItemButton
                sx={{
                  minHeight: 48,
                  justifyContent: props.open ? "initial" : "center",
                  px: 2.5,
                  borderRadius: 10,
                }}
                component="a"
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: props.open ? 3 : "auto",
                    justifyContent: "center",
                  }}
                >
                  {buttonIcon}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Typography
                      variant="subtitle1"
                      color={activeLink}
                      sx={{
                        width: "max-content",
                        maxWidth: 100,
                        whiteSpace: "pre-wrap",
                        wordWrap: "break-word",
                      }}
                    >
                      {data.text}
                    </Typography>
                  }
                  sx={{ opacity: props.open ? 1 : 0 }}
                />
              </ListItemButton>
            </Link>
          </ListItem>
        );
      })}

      <Divider sx={{ my: 2 }} />

      <ListItem disablePadding sx={{ display: "block" }}>
        <ListItemButton
          sx={{
            minHeight: 48,
            justifyContent: props.open ? "initial" : "center",
            px: 2.5,
            borderRadius: 10,
          }}
          onClick={handleProfileMenuOpen}
        >
          <ListItemIcon
            sx={{
              minWidth: 0,
              mr: props.open ? 2 : "auto",
              justifyContent: "center",
            }}
          >
            <UserAvatar />
          </ListItemIcon>
          <ListItemText
            primary={
              <Typography
                variant="subtitle1"
                sx={{
                  width: "max-content",
                  maxWidth: 150,
                  whiteSpace: "pre-wrap",
                  wordWrap: "break-word",
                }}
              >
                {`${user.firstName} ${user.lastName}`}
              </Typography>
            }
            sx={{ opacity: props.open ? 1 : 0 }}
          />
        </ListItemButton>
        <Menu
          id="basic-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          MenuListProps={{
            "aria-labelledby": "basic-button",
          }}
        >
          <Link href={`/profile/${user._id}`} passHref>
            <MenuItem component="a">Profile</MenuItem>
          </Link>
          <Link href="/account" passHref>
            <MenuItem component="a">My account</MenuItem>
          </Link>
          <MenuItem onClick={onLogout}>Logout</MenuItem>
        </Menu>
      </ListItem>
      <ListItem
        disablePadding
        sx={{ display: "block", mt: "auto", mb: 3, textAlign: "center" }}
      >
        <DarkModeSwitch />
      </ListItem>
    </List>
  );

  return drawer;
}
