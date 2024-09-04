import React from 'react'
import './PercentageChart.css'



export default function PercentageChart({percentage}) {
  return (
    <div class="pie animate" style={{"--p": `${percentage}`}} >{percentage}%</div>
  )
}
