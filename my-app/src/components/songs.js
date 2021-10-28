import Signup from './songs';
import React, { useEffect, useState } from 'react';

const Songs = () => {

    const [Song, setSong] = useState('');
    const [art, setArt] = useState([]);

    const [newsong, setNewsong] = useState('');
    const [newart, setNewart] = useState('');


    function handleSong(e){
        setSong(e.target.value);
    }

    function handleArt(e){
        setArt(e.target.value);
    }
    function handleNewsong(e){
        setNewsong(e.target.value);
    }

    function handleNewart(e){
        setNewart(e.target.value);
    }
    function handleSubmit(e){
        e.preventDefault();
        console.log(Song,art)
        fetch('http://127.0.0.1:5000/songs', {
            method: 'GET',
            data: {
                song: Song,
                artist: art
            }
        }).then(response => {
            console.log("success",response);
            // add logic to redirect to login if response is succeess
        }).catch(error => {
            console.log("failure",error);
        })
    }

    useEffect(() => {

        fetch('http://127.0.0.1:5000/spotify', {
            method: 'GET',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type':'application/json'
            }
        }).then(response => response.json())
        .then(response => {
                        if(response){
                console.log(response)
                const artist = response.artists;
                console.log(artist, 'artsits')
                setArt(artist);
            }
        })
        .catch(error => {
            console.log(error)
        })

        fetch('http://127.0.0.1:5000/lyrics', {
            method: 'GET',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type':'application/json'
            }
        }).then(response => response.json())
        .then(response => {
                        if(response){
                console.log(response)
    
            }
        })
        .catch(error => {
            console.log(error)
        })

    },[])

    return (
    
    <div class="container-full">
        <div class="row">
            <div class="col-lg-12 text-center v-center">
                {
                    art && art.map(artist => {
                        return (
                            <h1>Artist: {artist.name}</h1>
                        )
                    })
                }
                <h1>Find song here!</h1>
                <p class="lead">Find song page</p>

                <form class="col-lg-12" onSubmit={handleSubmit}>
                    <div class="input-group" style={{width:"340px",textAlign:"center",margin: "auto"}}>
                        <input onChange={handleSong} class="form-control input-lg" title="Please enter your email." placeholder="Enter your email" type="email" name="email"/>
                        <input onChange={handleArt} class="form-control input-lg" title="Please enter your password." placeholder="Enter your password" type="password" name="password"/>
                        <span class="input-group-btn"><button class="btn btn-lg btn-primary" type="submit">GO</button></span>
                    </div>
                </form>
            </div>
            <h1>Add song here!</h1>
                <p class="lead">Add song page</p>

                <form class="col-lg-12" onSubmit={handleSubmit}>
                    <div class="input-group" style={{width:"340px",textAlign:"center",margin: "auto"}}>
                        <input onChange={handleNewsong} class="form-control input-lg" title="Please enter your email." placeholder="Enter your email" type="email" name="email"/>
                        <input onChange={handleNewart} class="form-control input-lg" title="Please enter your password." placeholder="Enter your password" type="password" name="password"/>
                        <span class="input-group-btn"><button class="btn btn-lg btn-primary" type="submit">GO</button></span>
                    </div>
                </form>

        </div>
    </div>
  
    )
}

export default Songs;