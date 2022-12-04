import React from "react";
import classes from './InfoBar.module.css'
import {Progress, Typography} from "antd";

interface InfoBarPropsType {
    page: string
    responseData?: string
    isLoading?: boolean
}

const InfoBar: React.FC<InfoBarPropsType> = (props) => {
    return (
        <div className={classes.container}>
            <Typography className={classes.header}>Info:</Typography>
            <div className={classes.infoContent}>
                {props.isLoading
                    ? <Typography>Loading...</Typography>
                    : <>
                        <Typography>{props.responseData}</Typography>
                    </>
                }
            </div>


        </div>
    )
}

export default InfoBar;
