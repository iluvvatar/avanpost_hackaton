import React from "react";
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
    const [form] = Form.useForm();

    const onFinish = (values: any) => {
        console.log('Success:', values);
    };
    const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
    };
    const onSubmitHandler = () => {
        form.validateFields()
            .then((values: NewVersionFormValueTypes) => {
                console.log(values)
                createVersion(values);
                form.resetFields();
            })
            .catch((info) => {
                console.log('Validate Failed:', info);
            });
    }

    const createVersion = (values: NewVersionFormValueTypes) => {
        console.log('createVersion', values)
        axios.post(`http://158.160.47.53:8080/api/v1/versions/new?label=${values.label}&data_url=${values.dataUrl}`)
            .then(response => {
                console.log(response)
            })
            .catch(reject => {
                console.log(reject)
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
                           name="dara_url"
                           rules={[{required: true, message: 'Please paste link to images'}]}
                >
                    <Input placeholder="Paste link"/>
                </Form.Item>
                <Button type='primary'
                        onClick={onSubmitHandler}
                >
                    Start learning
                </Button>
            </Form>
            <InfoBar page={'learnPage'}/>
        </div>
    )
}

export default LearnPage;
