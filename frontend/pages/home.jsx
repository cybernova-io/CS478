import Layout from "../components/Layout";
import PostForm from "../components/post/PostForm";
import PostItem from "../components/post/PostItem";
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { getPosts, reset } from "../src/features/posts/postSlice";
import Spinner from "../components/Spinner";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function Home() {
  const router = useRouter();
  const dispatch = useDispatch();

  var user = useSelector((state) => state.auth);
  const { posts, isLoading, isError, message } = useSelector(
    (state) => state.posts
  );

  //if (process.browser) {
   // const cookieChecked = getCookie("token");
    //if (cookieChecked) {
     // if (localStorage.getItem("user")) {
      //  user = JSON.parse(localStorage.getItem("user"));
       // return user;
      //}
    //}
  //}

  useEffect(() => {
    if (isError) {
      console.log(message);
    }

    if (user) {
			dispatch(getPosts());

			return () => {
				dispatch(reset());
			};
		} else {
			router.push('/');
		}

  }, [user, router, isError, message, dispatch]);

  // if (isLoading) {
  // 	return <Spinner />;
  // }

  return (
    <Layout>
      <PostForm />
      {posts.length !== 0 ? (
        posts
          .slice(0)
          .reverse()
          .map((post) => <PostItem key={post._id} post={post} />)
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
