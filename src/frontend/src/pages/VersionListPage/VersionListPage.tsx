import React, {useEffect, useState} from "react";
import {NavLink} from "react-router-dom";
import {List, Typography} from "antd";
import classes from './VersionListPage.module.css'
import {ArrowLeftOutlined} from "@ant-design/icons";
import axios from "axios";


interface VersionListPropsType {

}

const VersionListPage: React.FC<VersionListPropsType> = (props) => {

    let [versionList, setVersionList] = useState<string[]>([])

    useEffect(() => {
        axios.get('http://158.160.47.53:8080/api/v1/versions/list')
            .then(response => {
                console.log(response)
                setVersionList(response.data.data)
            })
            .catch(err => {
                console.log(err)
            })
    }, [])

    return (
        <div className={classes.container}>
            <NavLink to='/'>
                <div className={classes.backBtn}>
                    <ArrowLeftOutlined/>
                </div>
            </NavLink>
            <List
                className={classes.list}
                header={
                    <div className={classes.listHeader}>
                        <h2>VersionList</h2>
                    </div>
                }
                dataSource={versionList}
                renderItem={(version) => (
                    <List.Item>
                        <Typography>{version}</Typography>
                    </List.Item>
                )}
            />
        </div>
    )
}

export default VersionListPage;
