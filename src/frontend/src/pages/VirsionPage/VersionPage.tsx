import React from 'react'
import {useParams} from "react-router-dom";

interface VersionPagePropsType {

}

const VersionPage: React.FC<VersionPagePropsType> = () => {
    const {id} = useParams()

    return (
        <>
            <h3>VersionPage</h3>
            <div>Version id: {id}</div>
            <div>Classes: some classes</div>
            <div>Metrics: some metrics</div>
        </>

)
}

export default VersionPage
