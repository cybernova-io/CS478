import Layout from "../components/Layout";
import PostForm from "../components/post/PostForm";
import PostList from '../components/post/PostList';
import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/router';
import { getPosts, reset } from '../src/features/posts/postSlice';
import Spinner from '../components/Spinner';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
export default function Home() {
	const router = useRouter();
	const dispatch = useDispatch();
	const { user } = useSelector((state) => state.auth);
	const { posts, isLoading, isError, message } = useSelector(
		(state) => state.posts
	);

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
	/*

	<Layout>
			<PostForm />
			{posts.length !== 0 ? (
				posts
					.slice(0)
					.reverse()
          .map((post) => <PostList key={post._id} post={post} />)
			) : (
				<Box sx={{ width: '100%', margin: 'auto', mt: 3 }}>
					<Typography variant='subtitle1' component='div' textAlign='center'>
						No posts yet.
					</Typography>
				</Box>
			)}
		</Layout>
		*/

	if (!posts) return <p>Loading...</p>

	return (
		<Layout>
		<PostForm />
		{posts.length !== 0 ? (
			posts
				.slice(0)
				.reverse()
	  .map((post) => <PostList key={post._id} post={post} />)
		) : (
			<Box sx={{ width: '100%', margin: 'auto', mt: 3 }}>
				<Typography variant='subtitle1' component='div' textAlign='center'>
					No posts yet.
				</Typography>
			</Box>
		)}
	</Layout>
		

		);
}