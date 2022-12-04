import React from "react";
import {NavLink} from "react-router-dom";
import {List, Pagination, Typography} from "antd";
import classes from './VersionListPage.module.css'
import {ArrowLeftOutlined} from "@ant-design/icons";

interface VersionListPropsType {
    versionList: string[]
}

const VersionListPage: React.FC<VersionListPropsType> = (props) => {


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
                dataSource={props.versionList.slice(0,4)}
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
