import React from 'react'
import { createUseStyles } from 'react-jss'
import ReactLoading from 'react-loading';


const useStyles = createUseStyles({
  processButton:props => ({
    width: '25vh',
    height: '12vh',
    fontSize: '4vh',
    backgroundColor: props.isLoading? 'moccasin' : 'orangered',
    color: props.isLoading? 'grey' : 'white',
    border: [3, 'solid', 'white'],
    borderRadius: '5vh'
  }),
  spinnerContainer: {
    textAlign: 'center'
  },
  spinner: {
    display: 'inline-block'
  }
})

const Button = (props) => {

  const classes = useStyles(props);
  const buttonText = "Process";

  return (
    <button 
      className={classes.processButton}
      onClick={props.onClick}
    >
        {props.isLoading ? 
           (<div className={classes.spinnerContainer}>
             <ReactLoading 
              className={classes.spinner}
              type={'spin'} 
              color={'darkslategrey'} 
              height={'8vh'} 
              width={'8vh'}/>
           </div>): 
          buttonText}
    </button>
  )
}

export default Button