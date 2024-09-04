import { shuffle } from 'lodash';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './CopyrightNotice.css';

function CopyrightNotice() {
  let location = useLocation();
  const [names, setNames] = useState([
    'Nikos Papakonstantopoulos',
    'Andreas Stamos',
    'Maria Lazou',
    'Konstantinos Pikoulas',
    'Paraskevi Kasioumi',
    'Stefanos Yiannakopoulos'
  ])
    ;

  useEffect(() => {setNames(shuffle(names))}, [location])

  return (<div class="copyrightnotice">
    &copy; 2023{new Date().getFullYear() !== 2023 && `-${+new Date().getFullYear()}`}   {names.join(', ')}
    </div>);
}

export default CopyrightNotice;

