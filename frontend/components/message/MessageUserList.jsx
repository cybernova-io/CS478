import * as React from "react";
import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import Avatar from "@mui/material/Avatar";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import ListItemButton from "@mui/material/ListItemButton";
import friendService from "../../src/features/friends/friendService";
import { Typography } from "@mui/material";
import Link from "next/link";
import { useRouter } from "next/router";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";

export default function MessageUserList(props) {
  const router = useRouter();

  const { user } = useSelector((state) => state.auth);
  var localIsDarkMode = JSON.parse(localStorage.getItem("isDarkMode"));

  const [allFriends, setAllFriends] = useState([]);

  // Get user friends
  const getAllFriends = async () => {
    if (user) {
      var userFriendsList = await friendService.getAllFriends(user.token);
      setAllFriends(userFriendsList);
    }
  };

  useEffect(() => {
    getAllFriends();
  }, []);

  return (
    (router.pathname === "/messages" ||
      router.pathname === "/messages/[id]") && (
      <Grid
        item
        xs={4}
        sx={
          router.pathname !== "/messages"
            ? {
                display: { xs: "none", sm: "none", md: "block" },
              }
            : {}
        }
      >
        <Box
          sx={{
            width: "100%",
            p: 2,
            zIndex: 99,
            position: "sticky",
            top: "0px",
            boxSizing: "border-box",
            backgroundColor: "inherit",
            borderRight: "1px solid",
            borderColor: localIsDarkMode
              ? "rgba(255, 255, 255, 0.12)"
              : "rgba(0, 0, 0, 0.12)",
            position: "sticky",
            top: "0px",
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Box>
            <Typography variant="h6">Messages</Typography>
          </Box>
          <List
            sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
          >
            {allFriends.map((data) => {
              const labelId = `checkbox-list-secondary-label-${data}`;
              return (
                <Link key={data._id} href={`/messages/${data._id}`} passHref>
                  <ListItem disablePadding>
                    <ListItemButton>
                      <ListItemAvatar>
                        <Avatar
                          alt={`Avatar n°${data + 1}`}
                          src={data.photo && `/uploads/${data.photo}`}
                        />
                      </ListItemAvatar>
                      <ListItemText
                        id={labelId}
                        primary={`${data.firstName} ${data.lastName}`}
                      />
                    </ListItemButton>
                  </ListItem>
                </Link>
              );
            })}
          </List>
        </Box>
      </Grid>
    )
  );
}
