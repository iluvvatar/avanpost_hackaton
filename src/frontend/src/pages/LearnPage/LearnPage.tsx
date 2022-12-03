import React from "react";
import {Button, Form, Input} from "antd";
import {NewVersionFormValueTypes} from "../../App";
import InfoBar from "../../components/InfoBar/InfoBar";
import classes from './LearnPage.module.css'
import {ArrowLeftOutlined} from "@ant-design/icons";
import {NavLink} from "react-router-dom";

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
                form.resetFields();
            })
            .catch((info) => {
                console.log('Validate Failed:', info);
            });
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
                           name="title"
                           rules={[{required: true, message: 'Please input title'}]}
                >
                    <Input placeholder='New version title'/>
                </Form.Item>
                <Form.Item label="Link"
                           name="link"
                           rules={[{required: true, message: 'Please paste link to images'}]}
                >
                    <Input placeholder="Paste link"/>
                </Form.Item>
                <Button type='primary'>
                    Start learning
                </Button>
            </Form>
            <InfoBar page={'learnPage'}/>
        </div>
    )
}

export default LearnPage;
