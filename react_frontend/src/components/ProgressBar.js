import React, {useState, useEffect} from 'react'
import '../css/ProgressBar.css'


export default function Progressbar(props) {
	
	// useEffect(() => {
	// 	if (props.filled) setFilled(props.filled)
	// 	console.log('Ustawiono progressbar')
	// }, [props.filled]) 

	console.log('ProgressBar rendered with parameter', props.filled)
	
 	return (
	  	<div className='progressbar-container'>
			<div className="progressbar" style={{
				height: "100%",
				width: `${props.filled}%`,
				backgroundColor: "orange",
			}}>
			<span className="progressPercent">{ props.filled }%</span>
			</div>
		</div>
  	)
}
