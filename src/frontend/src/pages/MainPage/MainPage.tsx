import React from "react";
import {Button} from "antd";
import classes from './MainPage.module.css'
import {NavLink} from "react-router-dom";
import {CheckCircleOutlined, InfoCircleOutlined} from "@ant-design/icons";

interface MainPagePropsType {

}

const MainPage: React.FC<MainPagePropsType> = (props) => {

    return (
        <div className={classes.mainPageContainer}>
            <NavLink to='/test'>
                <Button type='primary'
                        className={classes.mainPageBtn}
                >
                    <CheckCircleOutlined/>
                    <div>Test</div>
                </Button>
            </NavLink>
            <NavLink to="/learn">
                <Button type='primary'
                        className={classes.mainPageBtn}
                >
                    <InfoCircleOutlined />
                    <div>Learn</div>
                </Button>
            </NavLink>
        </div>

    )
}

export default MainPage
