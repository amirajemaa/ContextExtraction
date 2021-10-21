/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";

function DarkFooter() {
  return (
    <footer className="footer" data-background-color="black">
      <Container>
        <nav>
          <ul>
            <li>
             
                ENSI
             
            </li>
           
          </ul>
        </nav>
        <div className="copyright" id="copyright">
          © {new Date().getFullYear()}, doContext
          
            
         
          
        </div>
      </Container>
    </footer>
  );
}

export default DarkFooter;
