import React from 'react'
import { createUseStyles } from 'react-jss'

const useStyles = createUseStyles({
  inputBox: {
    color: 'black',
    width: '50vw',
    height: '20vh',
    fontSize: '4vh',
    resize: 'none',
    border: [2, 'solid', 'darkslategrey'],
    borderRadius: '5px',
    padding: '2vh'
  },
  inputBoxContainer: {
      margin: '4vh'
  }
})

const InputBox = (props) => {

  const classes = useStyles(props);
  let placeholder = "Enter Text Here...";

  return (
    <div className={classes.inputBoxContainer}>
      <textarea
        className={classes.inputBox}
        onChange={props.onChange}
        placeholder={placeholder}
      >
      </textarea>
    </div>
  )
}

export default InputBox