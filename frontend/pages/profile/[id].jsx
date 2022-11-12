import Layout from "../../components/Layout";
import PostForm from "../../components/post/PostForm";
import PostList from "../../components/post/PostList";
import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { getPosts } from "../../src/features/posts/postSlice";
import userService from "../../src/features/users/usersService";
import friendService from "../../src/features/friends/friendService";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import AvatarGroup from "@mui/material/AvatarGroup";
import Skeleton from "@mui/material/Skeleton";
import FriendOptions from "../../components/friends/FriendOptions";
import Link from "next/link";

ProfileId.title = "Screagles Connect: Profile";

export default function ProfileId() {
  const router = useRouter();
  const dispatch = useDispatch();
  const { id } = router.query;

  const { user } = useSelector((state) => state.auth);
  const { posts } = useSelector((state) => state.posts);

  const [userData, setUserData] = useState({
    firstName: "",
    lastName: "",
    photo: "",
    friends: "",
  });

  const [allFriends, setAllFriends] = useState([]);

  // Get user details by _id
  const getUserDetails = async () => {
    if (user) {
      const userData = await userService.getUserDataById(id, user.token);
      var newUserData = {
        _id: userData._id,
        lastName: userData.lastName,
        firstName: userData.firstName,
        photo: userData.photo,
      };

      setUserData(newUserData);
    }

    if (newUserData) {
      var userFriendsList = await friendService.getAllFriendsById(
        newUserData._id,
        user.token
      );
      setAllFriends(userFriendsList);
    }
  };

  useEffect(() => {
    getUserDetails();
    dispatch(getPosts());
  }, [user, JSON.stringify(userData), router, dispatch]);

  var isFriend = false;

  if (allFriends.length > 0 && user) {
    isFriend = allFriends.some((data) => data._id === user._id);
  }

  return (
    <Layout>
      <Box sx={{ px: 2, py: 1, width: "100%" }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={12}>
            <Stack
              spacing={2}
              direction="row"
              justifyContent="flex-start"
              alignItems="flex-start"
            >
              {userData.firstName !== "" && userData.firstName !== undefined ? (
                <>
                  <Avatar
                    sx={{
                      width: 150,
                      height: 150,
                    }}
                    src={userData.photo && `/uploads/${userData.photo}`}
                  />
                  <Stack spacing={1}>
                    <Typography variant="h4" sx={{ fontWeight: 600 }}>
                      {`${userData.firstName} ${userData.lastName}`}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ color: "#808080", fontWeight: 600 }}
                    >
                      {allFriends.length}
                      {allFriends.length > 1 ? " friends" : " friend"}
                    </Typography>
                    <AvatarGroup max={4} sx={{ width: "max-content" }}>
                      {allFriends.length > 0 &&
                        allFriends.map((data) => (
                          <Link
                            key={data._id}
                            href={`/profile/${data._id}`}
                            passHref
                          >
                            <Avatar
                              key={data._id}
                              alt={`${data.firstName} ${data.lastName}`}
                              src={data.photo && `/uploads/${data.photo}`}
                              title={`${data.firstName} ${data.lastName}`}
                              component="a"
                            />
                          </Link>
                        ))}
                    </AvatarGroup>
                  </Stack>
                  {user && user._id !== id && (
                    <Box sx={{ marginLeft: "auto !important", width: "19%" }}>
                      <FriendOptions
                        userData={userData}
                        component="likesModal"
                        sx={{ display: "none" }}
                      />
                    </Box>
                  )}
                </>
              ) : (
                <>
                  <Skeleton
                    variant="circular"
                    animation="wave"
                    width={150}
                    height={150}
                  />

                  <Stack spacing={1} sx={{ width: "40%" }}>
                    <Skeleton animation="wave" />
                    <Skeleton animation="wave" width="30%" />
                  </Stack>
                </>
              )}
            </Stack>
          </Grid>
        </Grid>
      </Box>
      {user && user._id === id && <PostForm />}
      {posts.length !== 0 && user ? (
        posts
          .slice(0)
          .reverse()
          .map(
            (post) =>
              ((post.user === userData._id && isFriend) ||
                (post.user === userData._id && post.audience === "Public") ||
                (post.user === userData._id && post.user === user._id)) && (
                <PostList key={post._id} post={post} />
              )
          )
      ) : (
        <Box sx={{ width: "100%", margin: "auto", mt: 3 }}>
          <Typography variant="subtitle1" component="div" textAlign="center">
            No posts yet.
          </Typography>
        </Box>
      )}
    </Layout>
  );
}
