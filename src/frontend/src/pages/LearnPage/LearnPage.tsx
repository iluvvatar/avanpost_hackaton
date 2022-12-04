import React, {useState} from "react";
import {Button, Form, Input} from "antd";
import {NewVersionFormValueTypes} from "../../App";
import InfoBar from "../../components/InfoBar/InfoBar";
import classes from './LearnPage.module.css'
import {ArrowLeftOutlined} from "@ant-design/icons";
import {NavLink} from "react-router-dom";
import axios from "axios";

interface LearnPagePropsType {

}

const LearnPage: React.FC<LearnPagePropsType> = (props) => {
    const [responseData, setResponseData] = useState<string>()
    const [isLoading, setIsLoading] = useState<boolean>()
    const [errorMessage, setErrorMessage] = useState<string>()
    const [form] = Form.useForm();

    const onFinish = (values: any) => {
        console.log('Success:', values);
        createVersion(values)
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
    };


    const createVersion = (values: NewVersionFormValueTypes) => {
        setIsLoading(true)
        console.log('createVersion', values)
        axios.post(`http://158.160.47.53:8081/api/v1/versions/new?label=${values.label}&data_url=${values.dataUrl}`)
            .then(response => {
                setResponseData(response.data)
                console.log(response)
            })
            .catch(reject => {
                setErrorMessage(JSON.stringify(reject.response.data.message))
                console.log(reject)
            })
            .finally(() => {
                setIsLoading(false)
            })
    }

    return (
        <div className={classes.container}
        >
            <NavLink to='/'>
                <div className={classes.backBtn}>
                    <ArrowLeftOutlined/>
                </div>
            </NavLink>
            <Form form={form}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  autoComplete="off"
                  className={classes.form}
            >
                <Form.Item label="Title"
                           name="label"
                           rules={[{required: true, message: 'Please input title'}]}
                >
                    <Input placeholder='New version title'/>
                </Form.Item>
                <Form.Item label="Link"
                           name="dataUrl"
                           rules={[{required: true, message: 'Please paste link to images'}]}
                >
                    <Input placeholder="Paste link"/>
                </Form.Item>
                <Button type='primary'
                        htmlType='submit'
                >
                    Start learning
                </Button>
            </Form>
            <InfoBar page={'learnPage'}
                     isLoading={isLoading}
                     responseData={responseData}
                     errorMessage={errorMessage}
            />
        </div>
    )
}

export default LearnPage;
