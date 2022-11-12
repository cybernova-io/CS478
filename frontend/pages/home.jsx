import Layout from "../components/Layout";
import PostForm from "../components/post/PostForm";
import PostList from "../components/post/PostList";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { getPosts } from "../src/features/posts/postSlice";
import Typography from "@mui/material/Typography";
import friendService from "../src/features/friends/friendService";
import Box from "@mui/material/Box";

Home.title = "Screagles Connect: Home";

export default function Home() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { posts, message } = useSelector((state) => state.posts);

  const [friendsData, setFriendsData] = useState([]);

  // Retrieves user's friends data
  const getUserFriends = async () => {
    if (user) {
      const userFriendsList = await friendService.getUserFriends(user.token);

      const friendDataArray = await Promise.all(
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
      setFriendsData(friendDataArray);
    }
  };
  useEffect(() => {
    dispatch(getPosts());
    getUserFriends();
  }, [user, message, dispatch]);

  // Checks for posts from user& friends
  var isPost = posts.map((post) => {
    return (
      (user && post.user === user._id) ||
      friendsData.some((e) => e.recipient == post.user && e.status === 3)
    );
  });

  return (
    <Layout>
      <PostForm />
      {isPost.includes(true) && user ? (
        posts
          .slice(0)
          .reverse()
          .map((post) => {
            if (
              post.user === user._id ||
              friendsData.some(
                (e) => e.recipient == post.user && e.status === 3
              )
            ) {
              return <PostList key={post._id} post={post} />;
            }
          })
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
