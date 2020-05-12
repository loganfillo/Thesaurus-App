import React, { useState } from 'react';
import InputBox from './InputBox'
import Button from './Button'
import OutputBox from './OutputBox'

import axios from 'axios'
import { createUseStyles } from 'react-jss'

const useStyles = createUseStyles({
  app: {
    textAlign: 'center'
  },
  appHeader: {
    fontSize: '2vh',
    backgroundColor: 'orangered',
    color: 'white',
    padding: '1vh'
  },
  appTitle: {
  },
  appBody: {
    minHeight: '100vh',    
    backgroundColor: 'lightblue',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  }
})


const App = (props) => {

  const classes = useStyles(props);

  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleInputTextChange = (event) => {
    setInputText(event.target.value);
  }

  const handleButtonClick = (event) => {
    const config = {
      method: 'post',
      url: '/process-text',
      data: {
        inputText: inputText
      }
    }
    setIsLoading(true);
    axios(config)
      .then(res => {
        setIsLoading(false);
        setOutputText(res.data.outputText);
      })
      .catch(err => {
        setIsLoading(false);
        console.log(err);
        alert(err)
      });
  }

  return (
    <div className={classes.app}>
      <header className={classes.appHeader}>
        <h1 className={classes.appTitle}>
          Thesaurus App
        </h1>
      </header>
      <header className={classes.appBody}>
        <InputBox onChange={handleInputTextChange}></InputBox>
        <Button isLoading={isLoading} onClick={handleButtonClick}></Button>
        <OutputBox isLoading={isLoading} text={outputText}></OutputBox>
      </header>
    </div>
  );
}

export default App;
