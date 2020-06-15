// IMPORT LIB
import React from 'react'

// CREATE A COMPONENT 
const TabHeader = ({children}) => {
    return(<ul className="nav nav-pills" id="myTab" role="tablist">
            {children}
        </ul>)
}

// EXPORT A COMPONENT
export default TabHeader;