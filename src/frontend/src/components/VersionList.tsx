import React from "react";
import {Version} from "../App";
import {Link} from "react-router-dom";

interface VersionListProps {
    versionList: Version[]
}

const VersionList: React.FC<VersionListProps> = (props) => {

    const versionElements = props.versionList.map(version => {
        return (
            <h3>
                <Link to={`/${version.id}`}>{version.title}</Link>
            </h3>
        )
    })

    return (
        <div>
            <h2>VersionList</h2>
            <div>{versionElements}</div>
        </div>
    )
}

export default VersionList;
