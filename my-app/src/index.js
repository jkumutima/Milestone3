import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './components/App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Signup from './components/signup';
import Login from './components/login';
import {Link} from 'react-router-dom';
import Song from './components/songs';

// var element = React.createElement('h1', { className: 'greeting' }, 'Hello, world!');
// ReactDOM.render(element, document.getElementById('root'));


ReactDOM.render(
 <React.StrictMode>
   <BrowserRouter>
   <div>
      <Link to="/">Home </Link>
      <Link to="/signup">Sign up</Link>
      <Link to="/login">Login </Link>
    </div>
  <Switch>
    <Route path='/' exact component={App}/>
    <Route path='/signup' exact component={Signup}/>
    <Route path='/login' exact component={Login}/>
    <Route path='/songs' exact component={Song}/>
    
  </Switch>
   </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log)) 
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
