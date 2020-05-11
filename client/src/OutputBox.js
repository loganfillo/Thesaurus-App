import React from 'react'
import { createUseStyles } from 'react-jss'

const useStyles = createUseStyles({
  outputBox: {
    color: 'black',
    width: '50vw',
    height: '15vh',
    fontSize: '4vh',
    resize: 'none',
    border: [2, 'solid', 'darkslategrey'],
    borderRadius: '5px',
    padding: '2vh'
  },
  outputBoxContainer: {
    margin: '4vh'
  }
})

const OutputBox = (props) => {

  const classes = useStyles(props);
  let placeholder = "It will show up here";

  return (
    <div className={classes.outputBoxContainer}>
      <textarea
        className={classes.outputBox}
        readOnly
        placeholder={placeholder}
        value={props.text}
      >
      </textarea>
    </div>
  )
}

export default OutputBox