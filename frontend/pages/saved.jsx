import Layout from "../components/Layout";
import PostList from "../components/post/PostList";
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { getPosts } from "../src/features/posts/postSlice";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

Saved.title = "Screagles Connect: Saved Posts";

export default function Saved() {
  const dispatch = useDispatch();

  const { user } = useSelector((state) => state.auth);
  const { posts, isError, message } = useSelector((state) => state.posts);

  useEffect(() => {
    if (isError) {
      console.log(message);
    }

    dispatch(getPosts());
  }, [user, isError, message, dispatch]);

  var savedPostNum = 0;

  if (user) {
    posts.map((post) => {
      post.saves.userId.some((id) => id === user._id) && savedPostNum++;
    });
  }

  return (
    <Layout>
      {posts.length !== 0 && savedPostNum > 0 ? (
        posts
          .slice(0)
          .reverse()
          .map(
            (post) =>
              post.saves.userId.some((id) => id === user._id) && (
                <PostList key={post._id} post={post} />
              )
          )
      ) : (
        <Box sx={{ width: "100%", margin: "auto", mt: 3 }}>
          <Typography variant="subtitle1" component="div" textAlign="center">
            No saved posts yet.
          </Typography>
        </Box>
      )}
    </Layout>
  );
}
