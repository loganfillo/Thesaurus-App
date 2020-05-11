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
    minHeight: '100vh',    
    backgroundColor: '#6495ED',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  }
})


const App = (props) => {

  const classes = useStyles(props);

  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("")

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
    axios(config)
      .then(res => {
        setOutputText(res.data.outputText);
      })
      .catch(err => {
        console.log(err);
      });
  }

  return (
    <div className={classes.app}>
      <header className={classes.appHeader}>
        <InputBox onChange={handleInputTextChange}></InputBox>
        <Button onClick={handleButtonClick}></Button>
        <OutputBox text={outputText}></OutputBox>
      </header>
    </div>
  );
}

export default App;
