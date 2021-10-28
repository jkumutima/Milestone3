import React, { useState } from 'react';

const Signup = () => {

    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');


    function handleEmail(e){
        setEmail(e.target.value);
    }

    function handlePwd(e){
        setPwd(e.target.value);
    }

    function handleSubmit(e){
        e.preventDefault();
        console.log(email,pwd)
        fetch('http://127.0.0.1:5000/signupu', {
            method: 'POST',
            data: {
                email: email,
                password: pwd
            }
        }).then(response => {
            console.log("success",response);
            // add logic to redirect to login if response is succeess
        }).catch(error => {
            console.log("failure",error);
        })
    }

    return (
    
    <div className="container-full">
        <div className="row">
            <div className="col-lg-12 text-center v-center">
                <h1>Signup here!</h1>
                <p className="lead">Signup page</p>

                <form className="col-lg-12" onSubmit={handleSubmit}>
                    <div className="input-group" style={{width:"340px",textAlign:"center",margin: "auto"}}>
                        <input onChange={handleEmail} className="form-control input-lg" title="Please enter your email." placeholder="Enter your email" type="email" name="email"/>
                        <input onChange={handlePwd} className="form-control input-lg" title="Please enter your password." placeholder="Enter your password" type="password" name="password"/>
                        <span className="input-group-btn"><button className="btn btn-lg btn-primary" type="submit">GO</button></span>
                    </div>
                </form>
            </div>

        </div>
    </div>
  
    )
}

export default Signup