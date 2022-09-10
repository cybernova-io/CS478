import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import Form from './components/Form'
import Container from 'react-bootstrap/Container';

export default function App(){

  return (
    <Container fluid className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/signup" element={<Form/>}/>
          </Routes>
        </BrowserRouter>
      </Container>
  );
}
