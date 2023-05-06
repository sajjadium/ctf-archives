import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function Navi(props) {
  props.authRequired()

  if(props.auth){
    return (
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand href="/">SafeNote</Navbar.Brand>
            <Nav className="me-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/note">Note</Nav.Link>
              <Nav.Link href="/login" onClick={() => localStorage.removeItem("token")}>Logout</Nav.Link>
            </Nav>
          </Container>
        </Navbar>
    );
  }
  else {
    return (
        <>
          <Navbar bg="dark" variant="dark">
            <Container>
              <Navbar.Brand href="/">SafeNote</Navbar.Brand>
              <Nav className="me-auto">
                <Nav.Link href="/">Home</Nav.Link>
                <Nav.Link href="/register">Register</Nav.Link>
                <Nav.Link href="/login">Login</Nav.Link>
              </Nav>
            </Container>
          </Navbar>
        </>
    );
  }
}

export default Navi;