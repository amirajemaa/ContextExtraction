import axios from 'axios';
import EditButton from 'react-edit-button';
import React,{Component} from 'react';
import EdiText from 'react-editext'
import  ChangeEvent  from 'react';
import {
	Card,CardHeader,CardBody,NavItem,NavLink,Nav,FormGroup,Input,TabContent,TabPane,Container,Row,Col,} from "reactstrap";
class Button extends React.Component {
    state = {
        details: [],
        texte: "",
        contexte: "",
    };
    constructor(props) {
      super(props);
      this.handleMouseHover = this.handleMouseHover.bind(this);
      this.state = {
        isHovering: false,
      };
      }
      toggleHoverState(state) {
        return {
         isHovering: !state.isHovering,
        };
        }
      handleMouseHover() {
        this.setState(this.toggleHoverState);
        }
    showFile = () => {
      if (window.File && window.FileReader && window.FileList && window.Blob) {
           var preview = document.getElementById('show-text');
           var file = document.querySelector('input[type=file]').files[0];
           var reader = new FileReader()
          
           var textFile = /text.*/;
  
           if (file.type.match(textFile)) {
              reader.onload = function (event) {
              preview.innerHTML=""
              preview.innerHTML = event.target.result;
              
              axios
            .post("http://localhost:8000/wel/", {
                
              texte: event.target.result,
              contexte : ""
            })

            
            .catch((err) => {});
            console.log("ok")
            }
            
              
            
         
          
           } else {
              preview.innerHTML = "<span class='error'>It doesn't seem to be a text file!</span>";
           }
           reader.readAsText(file);
  
     } else {
        alert("Your browser is too old to support HTML5 File API");
     }
  }
   
  
    renderSwitch = (param) => {
        switch (param + 1) {
            case 1:
                return "primary ";
            case 2:
                return "secondary";
            case 3:
                return "success";
            case 4:
                return "danger";
            case 5:
                return "warning";
            case 6:
                return "info";
            default:
                return "yellow";
        }
    };
    onSave = val => {
     
      this.setState({
    
        texte:"",
        contexte:""
    });
    console.log('Edited Value -> ', val,"this.state.texte",this.state.texte)
      axios
            .post("http://localhost:8000/wel/", {
                
                texte : "",
                contexte : val
            })

            
            .catch((err) => {});
    }
  
    handleInput = (e) => {
        this.setState({
            [e.target.name]: e.target.value,
        });
        console.log(this.state.texte)
    };
  
    handleSubmit = (e) => {
        e.preventDefault();
        console.log(this.state.texte)
        if (!(this.state.texte=="")){
        axios
            .post("http://localhost:8000/wel/", {
               texte: this.state.texte,
                contexte : this.state.contexte
           })

            
          .catch((err) => {});
           console.log("ok",this.state.texte)
          }
            let data;
            axios
            .get("http://localhost:8000/wel/")
            .then((res) => {
                data = res.data;
                this.setState({
                    details: data,
                    texte:data.texte,
                    contexte:data.contexte
                });
            })
            .catch((err) => {});
            console.log("ok")
    };
render() {

return (
<div>
<div className="section section-tabs" style={{backgroundColor: "rgb(209, 211, 214)" }} >
<div>
<Container>
               
               <Row>
               
                 <Col className="ml-auto mr-auto" md="10" xl="6">
                 <form onSubmit={this.handleSubmit}>
                   <p className="category">Enter your text or upload a text file
             <input type="file"  onChange={this.showFile} name="file" />
             </p>
                   <Card>
                     
                     <CardBody>
                       <TabContent
                         className="text-center"
                        
                       >
                        
                         <div id="inputs">
                
                 <p className="category">Original Text</p>
                 <Row>
                   <Col lg="8" sm="100">
                     
                     <FormGroup>
                     <textarea aria-label="With textarea" rows = "10" cols = "66.97" name = "texte" placeholder="Type your text" id="show-text"s  value={this.state.texte}
                            onChange={this.handleInput} >

                       </textarea>
                     
                       
                     </FormGroup>
             
     
             
             
                   </Col>  
             
                 </Row>
           
               </div>
                         
                       </TabContent>
               <p className="category">
               <input type="submit" onSubmit={this.handleSubmit}  value="Get the context"  />
              
               </p>
               
                     </CardBody>
                   </Card>
                   </form>
                 </Col>
                
     
     
                 <Col className="ml-auto mr-auto" md="10" xl="6">
           <br></br><br></br><br></br><br></br><br></br><br></br>
                   <p className="category" >The context is : <br></br></p>
                   <Card>
                     <CardBody>
                       <TabContent
                         className="text-center"
                       >
                 <Row>
                   <Col lg="8" sm="100">
                      <FormGroup>
                
                     <textarea rows = "2.5" cols = "66.97" placeholder="The context will be shown here"  readOnly id="show_context" value={this.state.contexte} name="contexte">
                       </textarea>
         <div className= "ajouterContexte">
         <div
          onMouseEnter={this.handleMouseHover}
          onMouseLeave={this.handleMouseHover}
		  
        >
          <EdiText
  type="text"
  inputProps={{
    placeholder: 'Type your proposition here',
   
    style: {
      backgroundColor: '#233C51',
      color: '#E6ECF1',
      fontWeight: 500,
      width: 850,
    },
    name: 'contexte'
  }}
  viewProps={{
    className: 'custom-view-class'
  }}
  onChange={this.handleInput}
  containerProps={{
    className: 'top-level-class',
    style: { marginTop: 5,
               }
  }}
  
  buttonsAlign='after'
  onSave={this.onSave}
 
/>
{
          this.state.isHovering &&
          <div>
            add context suggestion! 
          </div>
        }
</div>
             </div>
             
         
           
                     </FormGroup>
             
                   </Col>  
            
                 </Row>       
                       </TabContent>
                     </CardBody>
                     
                   </Card>
                  
                 </Col>
                 
               </Row>
              
             </Container>
      </div>


           
               
</div>

</div>
);
}
}

export default Button;

