//import lib
import React, {Component} from 'react'
//ROUTER
import {Redirect} from 'react-router';
//FORM
import FormGroup from '../bootstrap/form/FormGroup';
import Submit from '../bootstrap/form/Submit';
//FORM-FIELDS
import TextField from '../bootstrap/form/fields/TextField';
import PasswordField from '../bootstrap/form/fields/PasswordField';
//API
import myUniversity from '../../API/myUniversity';
import {Cookies} from 'react-cookie';
//CONTEXT
import {UserContext} from '../context/UserContext';

//create a component 
//TODO: OPTIMIZE CALL (SPINNER)
//TODO: FIX ON RELOAD
class LoginForm extends Component{

    constructor(props){
        super(props);

        this.cookies = new Cookies()

        this.state = {
            freshman: '',
            password: '',
            loginError: false,
            isAuth: this.cookies.get('isAuth') || false,
        }
    }

    onChangeFields = (event) => {
        this.setState({[event.target.name]:event.target.value});
    }

    onSubmit = async(event) => {
        event.preventDefault();

        //console.log('before submit',this.state.isAuth);
        let response;
        let isAuth;
        let userType;

        try{
            response = await myUniversity.post('/student/login', {
                matricola_studente: this.state.freshman,
                password_studente: this.state.password
            });
        }catch(error){
            console.log(`😱 There was an error: ${error}`);
            this.setState({loginError: true})
            isAuth = false
        }
        if(response.data.length !== 0){
            this.cookies.set('matricola_studente', this.state.freshman);
            this.cookies.set('password_studente',this.state.password);
            userType = 'student';
            isAuth = true
        }else{
            try{
                response = await myUniversity.post('/professor/login',{
                    matricola_docente: this.state.freshman,
                    password_docente: this.state.password
                });
            }catch(error){
                console.log(`😱 There was an error: ${error}`);
                this.setState({loginError: true})
                isAuth = false
            }

            if (response.data.length !== 0){
                this.cookies.set('matricola_docente', this.state.freshman);
                this.cookies.set('password_docente',this.state.password);
                userType='teacher';
                isAuth = true
            }else{
                this.setState({loginError: true})
                isAuth = false
            }
        }
        //console.log(response)
        this.cookies.set('isAuth',isAuth,{path:'/'});
        this.setState({isAuth: isAuth });
        this.context.update({[userType]:response.data[0]});
        console.log(this.context)

        //console.log('after submit',this.state.isAuth);
    }

    composeView = (isAuthenticated, error) => {
        if(!isAuthenticated){
            return (
                <form onSubmit={this.onSubmit}>
                    <h3>Login</h3>
                    <FormGroup>
                        <TextField
                        id='freshman'
                        name='freshman'
                        value={this.state.freshman}
                        onChange={this.onChangeFields}
                        placeholder='Matricola - Es. 0124002020'
                        required={true}
                        />
                    </FormGroup>
                    <FormGroup>
                        <PasswordField
                        id='password'
                        name='password'
                        value={this.state.password}
                        onChange={this.onChangeFields}
                        placeholder='Password'
                        required={true}
                        />
                    </FormGroup>
                    {error}
                    <Submit classColor='btn-primary'/>
                </form>
            );
        }else{
            return(<Redirect to={{pathname: "/"}}/>);
        }
    } 

    render(){
        const errorMessage = !this.state.loginError ? '' : <p className='text-danger'>Matricola o password errate</p>
        //console.log('login form',this.state.isAuth);
        //console.log('cookie form', this.cookies.get('isAuth'));

        return (
            <div>{this.composeView(this.state.isAuth,errorMessage)}</div>
        )
    }
}

LoginForm.contextType = UserContext;

//export a component
export default LoginForm;