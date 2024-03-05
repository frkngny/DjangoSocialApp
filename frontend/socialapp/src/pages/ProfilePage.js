import React, { useContext, useEffect, useState } from 'react'
import AuthContext from '../Utils/AuthUtil';
import useAxios from '../Utils/useAxios';
import { Card, CardContent, CardMedia, Grid, Typography } from '@mui/material';

function ProfilePage() {
    const { user, BASEURL } = useContext(AuthContext);
    const axios = useAxios();
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        axios.get(`${BASEURL}/profile/` + user.user_id).then((resp) => {
            console.log(resp.data)
            setProfile(resp.data);
        })
    }, []);

    return (
        <div className='page-container'>
            {
                profile !== null &&
                <Grid container spacing={1}>
                    <Grid item xs={3}>
                        <Card sx={{ display: 'flex', padding: '1lvh' }}>
                            <CardMedia component="img" sx={{ width: 160, display: { xs: 'none', sm: 'block' } }} image={profile.image} alt={profile.user.username}/>
                            <CardContent sx={{ flex: 1 }}>
                                <Typography component="h3" variant="h3" align={'center'}>{profile.full_name}</Typography>
                                <Typography variant="subtitle2" color="text.secondary" align={'center'}>{profile.user.username}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            }
        </div>
    )
}

export default ProfilePage