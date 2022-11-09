import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useSelector } from "react-redux";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import ListItemSecondaryAction from "@mui/material/ListItemSecondaryAction";
import friendService from "../src/features/friends/friendService";
import FriendOptions from "../components/friends/FriendOptions";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import { Typography } from "@mui/material";
import Grid from "@mui/material/Grid";
import FriendRequests from "../components/friends/FriendRequests";
import FriendSuggestions from "../components/friends/FriendSuggestions";
import UserNameLink from "../components/features/UserNameLink";

Friends.title = "Screagles Connect: Friends";

export default function Friends() {
  const { user } = useSelector((state) => state.auth);

  const [allFriends, setAllFriends] = useState([]);

  // Fetch all user's friend data
  const getAllFriends = async () => {
    if (user) {
      var userFriendsList = await friendService.getAllFriends(user.token);
      setAllFriends(userFriendsList);
    }
  };

  useEffect(() => {
    getAllFriends();
  }, [user, JSON.stringify(allFriends)]);

  return (
    <Layout>
      <Box sx={{ width: "100%", margin: "auto", pl: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  All Friends
                </Typography>
                <List sx={{ maxHeight: 500, overflow: "auto" }}>
                  {allFriends.map((data) => {
                    const labelId = `checkbox-list-secondary-label-${data._id}`;

                    return (
                      <ListItem key={data._id}>
                        <ListItemAvatar>
                          <Avatar
                            src={data.photo && `/uploads/${data.photo}`}
                          />
                        </ListItemAvatar>
                        <ListItemText
                          id={labelId}
                          primary={<UserNameLink data={data} />}
                        />
                        <ListItemSecondaryAction sx={{ width: "15%" }}>
                          <FriendOptions
                            userData={data}
                            component="allFriends"
                            componentFunc={() => getAllFriends()}
                          />
                        </ListItemSecondaryAction>
                      </ListItem>
                    );
                  })}
                  {allFriends.length === 0 && (
                    <Typography
                      gutterBottom
                      variant="body2"
                      component="span"
                      sx={{ color: "#808080" }}
                    >
                      No friends yet
                    </Typography>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sx={{ display: { sm: "block", md: "none" } }}>
            <FriendRequests />
          </Grid>
          <Grid item xs={12} sx={{ display: { sm: "block", md: "none" } }}>
            <FriendSuggestions />
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
}
