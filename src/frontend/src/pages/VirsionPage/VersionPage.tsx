import React from 'react'
import {useParams} from "react-router-dom";

interface VersionPageProps {

}

const VersionPage: React.FC<VersionPageProps> = () => {
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
