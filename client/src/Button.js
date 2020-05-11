import React from 'react'
import { createUseStyles } from 'react-jss'

const useStyles = createUseStyles({
  processButton: {
    width: '25vh',
    height: '12vh',
    fontSize: '4vh',
    backgroundColor: 'orangered',
    color: 'white',
    border: [3, 'solid', 'white'],
    borderRadius: '5vh'
  }
})

const Button = (props) => {

  const classes = useStyles(props);
  let buttonText = "Process";

  return (
    <button 
      className={classes.processButton}
      onClick={props.onClick}
    >
        {buttonText}
    </button>
  )
}

export default Button